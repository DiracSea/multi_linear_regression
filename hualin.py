from minibatch_sgd1.direct_minibatch import run
level = ('华林路晋安河','华林路YS3283260011','华林路YS3293240001','华林路YS3233270040','华林路YS3253270069')
for i in [1,2,5,10]:
    for j in [2,5]:
        for t in [15,30,60]:
            for l in level:
                run(i,j,t,200,200,0.02,l,10)
    