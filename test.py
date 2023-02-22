from tqdm import tqdm 
import time
pbar = tqdm(total=100)
for i in range(10):
   time.sleep(1)
   pbar.update(1)
pbar.close()
