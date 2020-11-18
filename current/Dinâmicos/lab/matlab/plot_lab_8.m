sigma_x_2 = @(x_1) (k_1 / k_2) * (y_r - x_1);

figure;
plot(linspace(0,1.5), sigma_x_2(linspace(0,1.5)), 'red');
hold on;
plot(out.x_1.data, out.x_2.data, 'blue');
hold off;

figure;
plot(out.x_1);
hold on;
plot(out.u);
hold off;