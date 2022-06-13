import time
import numpy as np
from typing import List, Dict

import torch
import torchaudio
import torchaudio.functional as F

import onnx
import onnxruntime


class Denoiser:
    def __init__(self, model_1, model_2):
        self.interpreter_1 = onnxruntime.InferenceSession(model_1)
        self.interpreter_2 = onnxruntime.InferenceSession(model_2)

    def denoise(self, filename, outputfile_name=None):
        return speech_enhancement_wav(filename, self.interpreter_1, self.interpreter_2, outputfile_name)


def speech_enhancement_wav(filename, interpreter_1, interpreter_2, outputfile_name=None):
    model_input_names_1 = [inp.name for inp in interpreter_1.get_inputs()]
    # preallocate input
    model_inputs_1 = {
        inp.name: np.zeros(
            [dim if isinstance(dim, int) else 1 for dim in inp.shape],
            dtype=np.float32)
        for inp in interpreter_1.get_inputs()}

    model_input_names_2 = [inp.name for inp in interpreter_2.get_inputs()]
    # preallocate input
    model_inputs_2 = {
        inp.name: np.zeros(
            [dim if isinstance(dim, int) else 1 for dim in inp.shape],
            dtype=np.float32)
        for inp in interpreter_2.get_inputs()}

    block_len = 512
    block_shift = 128
    # load audio file
    # audio,fs = sf.read(filename)
    waveform, fs = torchaudio.load(filename)
    audio = waveform.squeeze().numpy()
    # print(f"{audio.shape}, {waveform.squeeze().shape}")
    # check for sampling rate
    if fs != 16000:
        resampled_waveform = F.resample(waveform, fs, 16000, resampling_method="sinc_interpolation")
        audio = resampled_waveform.squeeze().numpy()
        fs = 16000
        # raise ValueError('This model only supports 16k sampling rate.')
    # preallocate output audio
    out_file = np.zeros((len(audio))).astype('float32')
    # create buffer
    in_buffer = np.zeros((block_len)).astype('float32')
    out_buffer = np.zeros((block_len)).astype('float32')
    # calculate number of blocks
    num_blocks = (audio.shape[0] - (block_len - block_shift)) // block_shift
    # iterate over the number of blcoks
    time_array = []
    for idx in range(num_blocks):
        start_time = time.time()
        # shift values and write to buffer
        in_buffer[:-block_shift] = in_buffer[block_shift:]
        in_buffer[-block_shift:] = audio[idx * block_shift:(idx * block_shift) + block_shift]
        # calculate fft of input block
        in_block_fft = np.fft.rfft(in_buffer)
        in_mag = np.abs(in_block_fft)
        in_phase = np.angle(in_block_fft)
        # reshape magnitude to input dimensions
        in_mag = np.reshape(in_mag, (1, 1, -1)).astype('float32')
        # set block to input
        model_inputs_1[model_input_names_1[0]] = in_mag
        # run calculation
        model_outputs_1 = interpreter_1.run(None, model_inputs_1)
        # get the output of the first block
        out_mask = model_outputs_1[0]
        # set out states back to input
        model_inputs_1[model_input_names_1[1]] = model_outputs_1[1]
        # calculate the ifft
        estimated_complex = in_mag * out_mask * np.exp(1j * in_phase)
        estimated_block = np.fft.irfft(estimated_complex)
        # reshape the time domain block
        estimated_block = np.reshape(estimated_block, (1, 1, -1)).astype('float32')
        # set tensors to the second block
        # interpreter_2.set_tensor(input_details_1[1]['index'], states_2)
        model_inputs_2[model_input_names_2[0]] = estimated_block
        # run calculation
        model_outputs_2 = interpreter_2.run(None, model_inputs_2)
        # get output
        out_block = model_outputs_2[0]
        # set out states back to input
        model_inputs_2[model_input_names_2[1]] = model_outputs_2[1]
        # shift values and write to buffer
        out_buffer[:-block_shift] = out_buffer[block_shift:]
        out_buffer[-block_shift:] = np.zeros((block_shift))
        out_buffer += np.squeeze(out_block)
        # write block to output file
        out_file[idx * block_shift:(idx * block_shift) + block_shift] = out_buffer[:block_shift]
        time_array.append(time.time() - start_time)

    # write to .wav file
    out_file = torch.from_numpy(out_file).unsqueeze(0)
    if outputfile_name is not None:
        torchaudio.save(outputfile_name, out_file, fs, format='mp3')
        # sf.write(outputfile_name, out_file, fs)
    print('Processing Time [ms]:')
    print(np.mean(np.stack(time_array)) * 1000)
    print('Processing finished.')
    return out_file, fs
