import cv

def getClusters(samples,labels):
    clusters = {}
    for i in xrange(0,samples.rows):
        v = samples[i,0]
        lbl = labels[i,0]
        try:
            clusters[lbl].append(v)
        except:
            clusters[lbl] = [ v ]
    return clusters

def kmeansUsingIntensity(im,k,iterations,epsilon):
    #create the samples and labels vector
    col = cv.Reshape(im, 1,im.width*im.height)
    samples = cv.CreateMat(col.height, 1, cv.CV_32FC1)
    cv.Scale(col,samples)

    labels = cv.CreateMat(col.height, 1, cv.CV_32SC1)
    crit = (cv.CV_TERMCRIT_EPS | cv.CV_TERMCRIT_ITER, iterations, epsilon)
    cv.KMeans2(samples, k, labels, crit)

    #calculate the means
    clusters = getClusters(samples,labels)

    means = {}
    for c in clusters:
        means[c] = sum(clusters[c])/len(clusters[c])

    for m in means:
        print m,means[m],len(clusters[m])

    #apply clustering to the image
    for i in xrange(0,col.rows):
        lbl = labels[i,0]
        col[i,0] = means[lbl]

def kmeansUsingIntensityAndLocation(im,k,iterations,epsilon):
    #create the samples and labels vector
    col = cv.Reshape(im, 1,im.width*im.height)
    samples = cv.CreateMat(col.height, 1, cv.CV_32FC3)
    count = 0
    for j in xrange(0,im.height):
        for i in xrange(0,im.width):
            value = (im[j,i],i,j)
            samples[count,0] = value
            count+=1


    labels = cv.CreateMat(col.height, 1, cv.CV_32SC1)
    crit = (cv.CV_TERMCRIT_EPS | cv.CV_TERMCRIT_ITER, iterations, epsilon)
    cv.KMeans2(samples, k, labels, crit)

    #calculate the means
    clusters = getClusters(samples,labels)

    means = {}
    for c in clusters:
        means[c] = 0
        for v in clusters[c]:
            means[c] += v[0]
        means[c] /= len(clusters[c])

    for m in means:
        print m,means[m],len(clusters[m])
    #apply clustering to the image
    for i in xrange(0,col.rows):
        lbl = labels[i,0]
        col[i,0] = means[lbl]

def kmeansUsingRGB(im,k,iterations,epsilon):
    col = cv.Reshape(im, 3,im.width*im.height)
    samples = cv.CreateMat(col.height, 1, cv.CV_32FC3)
    cv.Scale(col,samples)

    labels = cv.CreateMat(col.height, 1, cv.CV_32SC1)
    crit = (cv.CV_TERMCRIT_EPS | cv.CV_TERMCRIT_ITER, iterations, epsilon)
    cv.KMeans2(samples, k, labels, crit)
    #calculate the means
    clusters = getClusters(samples,labels)

    means = {}
    for c in clusters:
        means[c] = [0.0,0.0,0.0]
        for v in clusters[c]:
            means[c][0] += v[0]
            means[c][1] += v[1]
            means[c][2] += v[2]
        means[c][0] /= len(clusters[c])
        means[c][1] /= len(clusters[c])
        means[c][2] /= len(clusters[c])

    for m in means:
        print m,means[m],len(clusters[m])
    #apply clustering to the image
    for i in xrange(0,col.rows):
        lbl = labels[i,0]
        col[i,0] = means[lbl]

def kmeansUsingYUV(im,k,iterations,epsilon):
    cv.CvtColor(im,im,cv.CV_BGR2YCrCb)
    kmeansUsingRGB(im,k,iterations,epsilon)

#-------------------------------------------------------------
def kmeans(image_name,feature,k,iterations,epsilon):
    if feature == "INTENSITY":
        im = cv.LoadImageM(name,cv.CV_LOAD_IMAGE_GRAYSCALE)
        kmeansUsingIntensity(im,k,iterations,epsilon)
    elif feature == "INTENSITY+LOC":
        im = cv.LoadImageM(name,cv.CV_LOAD_IMAGE_GRAYSCALE)
        kmeansUsingIntensityAndLocation(im,k,iterations,epsilon)
    elif feature == "RGB":
        im = cv.LoadImageM(name,cv.CV_LOAD_IMAGE_COLOR)
        kmeansUsingRGB(im,k,iterations,epsilon)
    elif feature == "YUV":
        im = cv.LoadImageM(name,cv.CV_LOAD_IMAGE_COLOR)
        kmeansUsingYUV(im,k,iterations,epsilon)

    cv.ShowImage("win1",im)
    cv.WaitKey(0)

if __name__ == "__main__":
    name = "../test images/single object/189080.jpg"
    k = 3
    iterations = 100
    epsilon = 0.001

    print "img name =",name
    kmeans(name,"INTENSITY",k,iterations,epsilon)
    #kmeans(name,"INTENSITY+LOC",k,iterations,epsilon)
    #kmeans(name,"RGB",k,iterations,epsilon)
    #kmeans(name,"YUV",k,iterations,epsilon)
