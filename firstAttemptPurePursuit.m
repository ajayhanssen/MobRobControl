clear, close all

waypoints = [0,0; 1,1.5; 3,2; 4,4; 6,3];

controller = controllerPurePursuit;
controller.LookaheadDistance = 0.5;
controller.Waypoints = waypoints;

% pose = [x, y, theta]
x = 0.5;
y = -0.5;
psi = 0;
pose = [x, y, psi];

dt = 0.1;
N = 700;

figure
hold on, grid on, axis equal

% plot waypoinrts
plot(waypoints(:,1), waypoints(:,2), 'k--o')

% plot robot
robPlot = plot(x,y,'bo','MarkerSize',8,'MarkerFaceColor','b');
trajPlot = plot(x,y,'b');
lookaheadPlot = plot(0,0,'rx','MarkerSize',10);
headingArrow = quiver(x,y,0,0,'r','LineWidth',2);

traj = [x, y];

for iter = 1:N

    [vel, angvel, lookaheadpoint] = controller(pose);

    x = x + vel*cos(psi)*dt;
    y = y + vel*sin(psi)*dt;
    psi = psi + angvel*dt;

    pose = [x, y, psi];
    traj = [traj; x y];

    set(robPlot,'XData',x,'YData',y)
    set(trajPlot,'XData',traj(:,1),'YData',traj(:,2))
    set(lookaheadPlot,'XData',lookaheadpoint(1),'YData',lookaheadpoint(2))
    larr = 0.3;
    set(headingArrow,'XData',x,'YData',y,'UData',larr*cos(psi),'VData',larr*sin(psi))

    drawnow
end
