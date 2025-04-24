#include<iostream>
#include<algorithm>
#include<vector>
using namespace std;

class LRU{
    public:
    
        bool find(vector<int> memory, int page){
            for(int i = 0;i<memory.size();i++){
                if(memory[i] == page) return true;
            }
            return false;
        }
        
        void erase(vector<int> &memory, int num){
            
            int idx = 0;
            
            for(int i = 0;i<memory.size();i++){
                if(memory[i] == num){
                    idx = i;
                    break;
                }
            }
            
            memory.erase(memory.begin()+idx);
            return;
        }
    
    
        int pageFaults(int N, int C, int pages[]){
         
         
         vector<int> memory;
         int pageFault = 0;
         
         for(int i = 0;i<N;i++){
             
             bool inMemory = find(memory,pages[i]);
             
             if(inMemory) erase(memory,pages[i]);
             
             else{
                 
                 if(memory.size() >= C) memory.erase(memory.begin());
                 
                 pageFault++;
             }
             
             memory.push_back(pages[i]);
            }
            
            return pageFault;
         
    }
};

int main(){
    int N = 12, C = 5;
    int pages[] = {6,5,20,15,18,16,3,5,13,20,5,14};
    
    LRU lru;
    cout << lru.pageFaults(N, C, pages) << endl; 
    
    return 0;
}
    


