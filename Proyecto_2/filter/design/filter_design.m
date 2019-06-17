%This files calculates coefficients for a butterworth filter
%https://www.mathworks.com/help/signal/ref/butter.html#bucse3u-Wn

%Sampling freq
fs=2000;
%Cutoff freq
fc=10;
%Order of the filter
N=2;
%
Wn=fc/(fs/2);
%Coefficients
[B,A] = butter(N,Wn)

%Graph
%h = fvtool(B,A);

%B=1.0e-03 *[0.2414    0.4827    0.2414]
%A=1.0000   -1.9556    0.9565