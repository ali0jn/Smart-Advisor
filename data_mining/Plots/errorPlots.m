function p = plotError(x, y1, y2, y3, y4, y5, y6, t)
    figure("Position", [10 10 1800 1200])
    p = plot(x,y1,x,y2,x,y3,x,y4,x,y5,x,y6);
    legend([p(1) p(2) p(3) p(4) p(5) p(6)], {'MAE Train','MAE Test','MSE Train', 'MSE Test','R2 Train', 'R2 Test'})
    a = get(gca,"XTickLabel");
    b = get(gca,"YTickLabel");
    set(gca, "XTickLabel", a,"fontsize", 20);
    set(gca, "YTickLabel", b,"fontsize", 20);
    p(1).LineWidth = 2;
    p(2).LineWidth = 2;
    p(3).LineWidth = 2;
    p(4).LineWidth = 2;
    p(5).LineWidth = 2;
    p(6).LineWidth = 2;
    p(1).LineStyle = "-";
    p(1).Marker = "*";
    p(2).LineStyle = "--";
    p(2).Marker = "d";
    p(3).LineStyle = "-.";
    p(3).Marker = "h";
    p(4).LineStyle = ":";
    p(4).Marker = "p";
    p(5).LineStyle = "-";
    p(5).Marker = "x";
    p(6).LineStyle = "-.";
    p(6).Marker = "s";
    ylabel("Error", "FontSize",20);
    xlabel("Number of Training Semesters", "FontSize",20);
    print(t,'-dsvg')
    

    
end
