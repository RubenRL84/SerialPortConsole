
y = load('Log.txt');


x= []



for v =0.0:+1.0:length(y)
  
   x = [x, v]; 
end
x = x'
x(1,:) = []

%y(1:8000,:) = []

f = 120e3/2*linspace(-1, 1, length(y));

figure(1)
plot(x,y)

figure(2)
plot(f,abs(fft(y)))


%y = exp(-1j*2*pi*f.*X);
figure(3)
z = exp(-1j*2*pi*60e3.*y)
plot(abs(fft(z)));



