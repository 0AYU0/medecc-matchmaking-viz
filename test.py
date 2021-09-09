library(plotly)
library(dplyr)
library(htmlwidgets)
library(widgetframe)
library(stringr)
library(htmltools)

df <- data.frame(lab = c("Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"),
            par= c("", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve"),
            ID = c(1,11,12,121,122,13,14,141,15),
            parentID =c(NA,1,1,12,12,1,1,14,1),
            val = c(10, 14, 12, 10, 2, 6, 6, 4, 4))

fig2 <- plot_ly(ids=df$ID,
               labels = df$lab,
               parents = df$parentID,
               values = df$val,
               type = 'sunburst',
               maxdepth=2,
               hovertemplate = paste('%{label}','<br>%{value} EUR<extra></extra>','<br>Anteil an %{parent}','%{percentParent: .1%}'),
                            )
fig2