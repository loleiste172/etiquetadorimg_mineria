#imports
from math import floor
from tkinter import *
import os
from tkinter import messagebox
import tkinter
from tkinter.filedialog import askdirectory, askopenfilename
import cv2
from matplotlib import image
import numpy as np
from PIL import Image
from PIL import ImageTk
import imutils
from skimage.feature import graycomatrix, graycoprops

def pxmy_calc(glcm, ngl, k):
    '''
    Returns p_x-y(k)
    Inputs  : glcm (single normalized gray level co. matrix)
              ngl (int, # gray levels)
              k (int, abs diff of i and j)
    Outputs : p_minus
    '''
    p_minus = 0
    # Add to p_x+y if i+j=k
    for i in range(0, ngl-1):
            for j in range(0, ngl-1):
                if abs(i-j) == k:
                    p_minus += glcm[i][j]
                else:
                    p_minus += 0
    return p_minus


def glcm_contrast(glcms_dict, ngl):
    '''
    Returns directionally-averaged Haralick contrast
    Inputs  : glcms_dict (dict of directional matrices)
    Ouputs  : mean of contrast_list
    '''
    # Initialize features list
    contrast_list = []
    # Iterate across glcms
    for key in glcms_dict:
        glcm = glcms_dict[key]
        n_glcm = glcm / np.sum(glcm)
        contrast = 0
        # Iterate across k, call pxmy_calc
        for k in range(0, ngl-1):
            contrast += (k**2) * pxmy_calc(n_glcm, ngl, k)
        contrast_list.append(contrast)
    # Return average contrast value
    return contrast_list[0],contrast_list[1],contrast_list[2],contrast_list[3]

def glcm_stat_calc(glcm, ngl):
    '''
    Returns means and standard deviations for single GLCM
    Inputs  : glcm (single normalized gray level co. matrix)
              ngl (int, # gray levels)
    Outputs : entropy
    '''
    # Calculate mean values
    mux, muy = 0, 0
    for i in range(0, ngl-1):
        for j in range(0, ngl-1):
            val = glcm[i][j]
            mux += i * val
            muy += j * val
    # Calculate standard deviations
    varx, vary = 0, 0
    for i in range(0, ngl-1):
        for j in range(0, ngl-1):
            val = glcm[i][j]
            varx += (i-mux)**2 * val
            vary += (j-muy)**2 * val
    sigx = np.sqrt(varx)
    sigy = np.sqrt(vary)
    return mux, muy, sigx, sigy

def glcm_correlation(glcms_dict, ngl):
    '''
    Returns directionally-averaged Haralick correlation
    Inputs  : glcms_dict (dict of directional matrices)
    Ouputs  : mean of corr_list
    '''
    # Initialize features list
    corr_list = []
    # Iterate across glcms
    for key in glcms_dict:
        glcm = glcms_dict[key]
        n_glcm = glcm / np.sum(glcm)
        # Get means and standard devs wrt x and y
        meanx, meany, stdx, stdy = glcm_stat_calc(n_glcm, ngl)
        # Calculate correlation
        inner = 0
        for i in range(0, ngl-1):
            for j in range(0, ngl-1):
                inner += (n_glcm[i][j] * i * j)
        corr = (inner - meanx*meany) / (stdx*stdy)
        corr_list.append(corr)
    # Return average entropy value
    #print("Correlacion de manera manual " + str(corr_list[0]))
    return np.mean(corr_list)
    
def quant_img(img, q):
    '''
    Quantizes image from 0 to nlevels-1
    Inputs  : img (grayscale image)
              q (number of quantization levels, int)
    Ouputs  : qimg(quantized image)
    '''
    # Check for grayscale image
    if len(img.shape) > 2:
        print("Input grayscale image")
        return
    # Quanization
    qimg = np.uint8(np.double(img)/255 * (q-1))
    return qimg

def get_glcms(img, levels, dist):
    '''
    Make GLCM (0, 45, 90, 135 deg)
    Inputs  : img (grayscale image)
              levels (quantization level, int)
              dist (distance between values, int)
    Outputs : glcm_dict
    '''
    # Check for grayscale image
    if len(img.shape) > 2:
        print("Input grayscale image")
        return
    # Quantize image, initialize matrices
    qimg = quant_img(img, levels)
    P0 = np.zeros((levels, levels), dtype=int)
    P45 = np.zeros((levels, levels), dtype=int)
    P90 = np.zeros((levels, levels), dtype=int)
    P135 = np.zeros((levels, levels), dtype=int)
    # Build 0 degree GLCM
    for i in range(0, qimg.shape[0]-1):
        for j in range(0, qimg.shape[1]-dist-1):
            gl0 = qimg[i][j]
            gl1 = qimg[i][j+dist]
            P0[gl0][gl1] += 1
    # Build 45 degree GLCM
    for i in range(dist, qimg.shape[0]-1):
        for j in range(0, qimg.shape[1]-dist-1):
            gl0 = qimg[i][j]
            gl1 = qimg[i-dist][j+dist]
            P45[gl0][gl1] += 1
    # Build 90 degree GLCM
    for i in range(dist, qimg.shape[0]-1):
        for j in range(0, qimg.shape[1]-1):
            gl0 = qimg[i][j]
            gl1 = qimg[i-dist][j]
            P90[gl0][gl1] += 1
    # Build 135 degree GLCM
    for i in range(dist, qimg.shape[0]-1):
        for j in range(dist, qimg.shape[1]-1):
            gl0 = qimg[i][j]
            gl1 = qimg[i-dist][j-dist]
            P135[gl0][gl1] += 1
    # Return glcms as dict
    glcm_dict = {'P0':P0, 'P45':P45, 'P90':P90, 'P135':P135}
    return glcm_dict

def glcm_entropy_calc(glcm, ngl):
    '''
    Returns entropy for single glcm
    Inputs  : glcm (single normalized gray level co. matrix)
              ngl (int, # gray levels)
    Outputs : entropy
    '''
    entropy = 0
    # Iterate across i, and j
    for i in range(0, ngl-1):
        for j in range(0, ngl-1):
            val = glcm[i][j]
            if val == 0.0:
                entropy += 0
            else:
                entropy -= val * np.log2(val)
    return entropy


def glcm_entropy(glcms_dict, ngl):
    '''
    Returns directionally-averaged Haralick entropy
    Inputs  : glcms_dict (dict of directional matrices)
    Ouputs  : mean of entropy_list
    '''
    # Initialize features list
    entropy_list = []
    # Iterate across glcms
    for key in glcms_dict:
        glcm = glcms_dict[key]
        n_glcm = glcm / np.sum(glcm)
        entropy_list.append(glcm_entropy_calc(n_glcm, ngl))
    # Return average entropy value
    return entropy_list[0], entropy_list[1], entropy_list[2], entropy_list[3]

def glcm_energy(glcms_dict, ngl):
    '''
    Returns directionally-averaged Harlick energy
    Inputs  : glcms_dict (dict of directional matrices)
    Ouputs  : mean of energy_list
    '''
    # Initialize features list
    energy_list = []
    # Iterate across glcms
    for key in glcms_dict:
        glcm = glcms_dict[key]
        n_glcm = glcm / np.sum(glcm)
        asm = 0
        # Iterate across i and j
        for i in range(0, ngl-1):
            for j in range(0, ngl-1):
                asm += (n_glcm[i][j]) * (n_glcm[i][j])
        energy_list.append(np.sqrt(asm))
    # Return average ASM value
    return energy_list[0],energy_list[1],energy_list[2],energy_list[3]

    
def glcm_homogeneity(glcms_dict, ngl):
    '''
    Returns directionally-averaged Haralick homogeneity (IDM)
    Inputs  : glcms_dict (dict of directional matrices)
    Ouputs  : mean of homog_list
    '''
    # Initialize features list
    homog_list = []
    # Iterate across glcms
    for key in glcms_dict:
        glcm = glcms_dict[key]
        n_glcm = glcm / np.sum(glcm)
        homog = 0
        # Iterate across i, and j
        for i in range(0, ngl-1):
            for j in range(0, ngl-1):
                front = 1 / (1 + (i-j)**2)
                homog += front * n_glcm[i][j]
        homog_list.append(homog)
    # Return average homogeneity value
    return homog_list[0],homog_list[1],homog_list[2],homog_list[3]



def glcm_diffentropy(glcms_dict, ngl):
    '''
    Returns directionally-averaged Haralick difference entropy
    Inputs  : glcms_dict (dict of directional matrices)
    Ouputs  : mean of diffentropy_list
    '''
    # Initialize features list
    diffentropy_list = []
    # Iterate across glcms
    #for key in glcms_dict:
    glcm = glcms_dict['P0']
    n_glcm = glcm / np.sum(glcm)
    # Calculate sum entropy
    diffentropy = 0
    for k in range(0, ngl-1):
        val = pxmy_calc(n_glcm, ngl, k)
        if val == 0.0:
            diffentropy += 0
        else:
            diffentropy -= val * np.log2(val)
    diffentropy_list.append(diffentropy)
    # Return average contrast value
    return np.mean(diffentropy_list)

def glcm_asm(glcms_dict, ngl):
    '''
    Returns directionally-averaged angular second moment (asm)
    Inputs  : glcms_dict (dict of directional matrices)
    Ouputs  : mean of asm_list
    '''
    # Initialize features list
    asm_list = []
    # Iterate across glcms
    for key in glcms_dict:
        glcm = glcms_dict[key]
        n_glcm = glcm / np.sum(glcm)
        asm = 0
        # Iterate across i and j
        for i in range(0, ngl-1):
            for j in range(0, ngl-1):
                asm += (n_glcm[i][j]) * (n_glcm[i][j])
        asm_list.append(asm)
    # Return average ASM value
    return asm_list[0],asm_list[1],asm_list[2],asm_list[3]

def glcm_variance(glcms_dict, ngl):
    '''
    Returns directionally-averaged Haralick variance
    Inputs  : glcms_dict (dict of directional matrices)
    Ouputs  : mean of var_list
    '''
    # Initialize features list
    var_list = []
    # Iterate across glcms
    for key in glcms_dict:
        glcm = glcms_dict[key]
        n_glcm = glcm / np.sum(glcm)
        # Get means and standard devs wrt x and y
        meanx, meany, _stdx, _stdy = glcm_stat_calc(n_glcm, ngl)
        meanxy = (meanx + meany) / 2.0
        # Calculate correlation
        var = 0
        for i in range(0, ngl-1):
            for j in range(0, ngl-1):
                var += ((i - meanxy)**2 * n_glcm[i][j])
        var_list.append(var)
    # Return average entropy value
    return np.mean(var_list)