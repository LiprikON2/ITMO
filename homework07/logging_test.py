import logging
import multiprocessing

def run():
    BARCLASS = Bar()
    BARCLASS.bar()


class Bar(object):
    def bar(self):
        print('fired bar')
        self.logg = logging.getLogger(__name__)
        
        self.logg.info('Hi, bar')   
if __name__ == '__main__':       
    
    logging.basicConfig(
            filename=None,
            level=logging.INFO,
            format="%(name)s: %(process)d %(message)s")
    
    # LOGGING WORK
    run()


    # LOGGING DOESNT WORK
    # for _ in range(1):
    #    
    #     p = multiprocessing.Process(target=run)
    #     p.start()
    #     p.join()
    #
    # my solution: just put basic config inside run()