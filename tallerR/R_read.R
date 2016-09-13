
folders<-list.files(path = "world-cup")
for (i in 1:20)
{
        x<-read.table(paste0(getwd(),"/world-cup/",folders[i],"/cup.txt"), sep="\t", 
                              encoding = "UTF-8", comment.char = "#")
        assign(paste0('data', folders[i]),x)
}
