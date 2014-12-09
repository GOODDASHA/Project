from numpy import *
def transposeLinkMatrix(outGoingLinks = [[]]):
        """
        Transpose the link matrix. The link matrix contains the pages each page points to.
        However, what we want is to know which pages point to a given page. However, we
        will still want to know how many links each page contains (so store that in a separate array),
        as well as which pages contain no links at all (leaf nodes).
 
        @param outGoingLinks outGoingLinks[ii] contains the indices of pages pointed to by page ii
        @return a tuple of (incomingLinks, numOutGoingLinks, leafNodes)
        """
 
        nPages = len(outGoingLinks)
        # incomingLinks[ii] will contain the indices jj of the pages linking to page ii
        incomingLinks = [[] for ii in range(nPages)]
        # the number of links in each page
        numLinks = zeros(nPages, int32)
        print numLinks
        # the indices of the leaf nodes
        leafNodes = []
 
        for ii in range(nPages):
                if len(outGoingLinks[ii]) == 0:
                        leafNodes.append(ii)
                else:   
                        numLinks[ii] = len(outGoingLinks[ii])
                        # transpose the link matrix
                        for jj in outGoingLinks[ii]:
                                incomingLinks[jj].append(ii)
                        
        incomingLinks = [array(ii) for ii in incomingLinks]
        numLinks = array(numLinks)
        leafNodes = array(leafNodes)

        print incomingLinks, numLinks
        return incomingLinks, numLinks, leafNodes



def pageRankGenerator(
        At = [array((), int32)],
        numLinks = array((), int32),
        ln = array((), int32),
        alpha = 0.85,
        convergence = 0.01,
        checkSteps = 10
        ):
        """
        Compute an approximate page rank vector of N pages to within some convergence factor.
        @param At a sparse square matrix with N rows. At[ii] contains the indices of pages jj linking to ii.
        @param numLinks iNumLinks[ii] is the number of links going out from ii. 
        @param ln contains the indices of pages without links
        @param alpha a value between 0 and 1. Determines the relative importance of "stochastic" links.
        @param convergence a relative convergence criterion. smaller means better, but more expensive.
        @param checkSteps check for convergence after so many steps
        """
 
        # the number of "pages"
        N = len(At)
        
        # the number of "pages without links"
        M = ln.shape[0]

        # initialize: single-precision should be good enough
        iNew = ones((N,), float32) / N
        iOld = ones((N,), float32) / N
 
        done = False
        while not done:
                # normalize every now and then for numerical stability
                iNew /= sum(iNew)

                for step in range(checkSteps):
 
                        # swap arrays
                        iOld, iNew = iNew, iOld
                        #iOld = iNew
                        # an element in the 1 x I vector. 
                        # all elements are identical.
                        #print sum(iOld)
                        oneIv = (1 - alpha) * sum(iOld) / N
                        # an element of the A x I vector.
                        # all elements are identical.
                        oneAv = 0.0
                        if M > 0:
                                oneAv = alpha * sum(iOld.take(ln, axis = 0)) / N
                        # the elements of the H x I multiplication
                        for ii in range(N):
                                page = At[ii]
                                h = 0
                                if page.shape[0]:
                                        h = alpha * dot(iOld.take(page, axis = 0), 1. / numLinks.take(page, axis = 0))
                                iNew[ii] = h + oneAv + oneIv

                diff = iNew - iOld
                done = (sqrt(dot(diff, diff)) / N < convergence)
 
                yield iNew

def pageRank(
        linkMatrix = [[]],
        alpha = 0.85,
        convergence = 0.00001,
        checkSteps = 1
        ):
        """
        Convenience wrap for the link matrix transpose and the generator.
        """
        incomingLinks, numLinks, leafNodes = transposeLinkMatrix(linkMatrix)

        for gr in pageRankGenerator(incomingLinks, numLinks, leafNodes, 
                       alpha = alpha, 
                       convergence = convergence, 
                       checkSteps = checkSteps):
                final = gr
        return final

'''
links = [
                [1, 2],
                [2],
                [3],
                [4],
                [0]
        ]
 
print pageRank(links)
'''
import operator
x = {1: 2, 3: 4, 4:3, 2:1, 0:0}
sorted_x = sorted(x.items(), key=operator.itemgetter(1), reverse=True)
for k, v in sorted_x:
        print k, v
