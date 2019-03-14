import time, glob, subprocess
from queue import Queue
from threading import Thread

NUM_WORKER_THREADS = 8

# ----------------------------------------------------------

def find_worker(worker_number):

    print('Worker', worker_number, 'running')
    
    while not q.empty():
        
        start_time = time.time()
        
        id_to_find = q.get()

        print('Doing', id_to_find, 'worker', worker_number)
        
        results = subprocess.getoutput('grep ' + id_to_find + ' /mnt/ramdisk/GROUPED.all_shingles.tsv')
        n_found = len(results.strip().split('\n'))

        f = open('/home/spenteco/temp.text_reuse/everything_to_everything/' + id_to_find + '.tsv', 'w', encoding='utf-8')
        f.write(results + '\n')
        f.close()        
        
        q.task_done()

        stop_time = time.time()
    
# ----------------------------------------------------------

q = Queue()

for path_to_file in glob.glob('/home/data/eebo_process/adorned/*.xml'):
    q.put(path_to_file.split('/')[-1].split('.')[0])
    
total_start_time = time.time()
    
for a in range(NUM_WORKER_THREADS):
    print('Starting worker', a)
    t = Thread(target=find_worker, args=(a,))
    t.daemon = True
    t.start()

q.join()

print('time:', (time.time() - total_start_time))

print('Done!')
