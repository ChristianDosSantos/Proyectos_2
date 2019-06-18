%This files calculates coefficients for a butterworth filter
%https://www.mathworks.com/help/signal/ref/butter.html#bucse3u-Wn

%Sampling freq
fs=2000;
%Cutoff freq
fc=5;
%Order of the filter
N=10;
%
Wn=fc/(fs/2);
%Coefficients
[B,A] = fir1(N,Wn)
round(B*1000)

%Graph
h = fvtool(B,A);

%B=1.0e-03 *[0.2414    0.4827    0.2414]
%A=1.0000   -1.9556    0.9565
