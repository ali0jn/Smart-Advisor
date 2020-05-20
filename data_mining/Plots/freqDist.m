function p = plotFreq(x, y, t)
    figure("Position", [10 10 1800 1200]);
    p = bar(x,y);
    a = get(gca,"XTickLabel");
    b = get(gca,"YTickLabel");
    set(gca, "XTickLabel", a,"fontsize", 20);
    set(gca, "YTickLabel", b,"fontsize", 20);
    ylabel("Frequency", "FontSize",20);
    xlabel("Letter Grade Categories", "FontSize",20);
    print(t,'-dsvg')    
end
