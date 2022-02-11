
y = load('Log.txt');


x= []



for v =0.0:+1.0:12784
   
   x = [x, v]; 
end
x = x'
x(1:8001,:) = []

y(1:8000,:) = []

f = 30e3/2*linspace(-1, 1, length(y));

figure(1)
plot(x,y)

figure(2)
plot(f,abs(fft(y)))


%y = exp(-1j*2*pi*f.*X);
figure(3)
z = exp(-1j*2*pi*30e3.*y)
plot(abs(fft(z)));



