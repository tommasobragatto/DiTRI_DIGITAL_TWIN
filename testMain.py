import multiprocessing
from W3_P import W3_P
from W3_Q import W3_Q
from W3_V import W3_V
from W4_P import W4_P
from W4_Q import W4_Q
from W4_V import W4_V
from W5_P import W5_P
from W5_Q import W5_Q
from W5_V import W5_V
from W6_P import W6_P
from W6_Q import W6_Q
from W6_V import W6_V


def testMain():
    #if __name__ == '__main__':

        p1 = multiprocessing.Process(target=W6_P)
        p2 = multiprocessing.Process(target=W6_Q)
        p3 = multiprocessing.Process(target=W6_V)
        p4 = multiprocessing.Process(target=W5_P)
        p5 = multiprocessing.Process(target=W5_Q)
        p6 = multiprocessing.Process(target=W5_V)
        p7 = multiprocessing.Process(target=W4_P)
        p8 = multiprocessing.Process(target=W4_Q)
        p9 = multiprocessing.Process(target=W4_V)
        p10 = multiprocessing.Process(target=W3_P)
        p11 = multiprocessing.Process(target=W3_Q)
        p12 = multiprocessing.Process(target=W3_V)

        p1.start()
        p2.start()
        p3.start()
        p4.start()
        p5.start()
        p6.start()
        p7.start()
        p8.start()
        p9.start()
        p10.start()
        p11.start()
        p12.start()

        p1.join()
        p2.join()
        p3.join()
        p4.join()
        p5.join()
        p6.join()
        p7.join()
        p8.join()
        p9.join()
        p10.join()
        p11.join()
        p12.join()

if __name__ == '__main__':

     testMain()