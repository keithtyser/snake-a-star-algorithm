SnakeAIPath="../SnakeAI"
search_depth=3
clang -c Snake.c -O3 -I/opt/homebrew/include/ -D_THREAD_SAFE -L/opt/homebrew/lib -lSDL2
if [  $# -gt 0 ] 
  then
  if [ $1 -eq 0 ]
  then
    nvcc -c $SnakeAIPath/*.cu $SnakeAIPath/probabilistic_heuristic.c $SnakeAIPath/utility.c -O3 -I ./includes/ -I ./  -I $CUDA_PATH/include -arch=sm_61 -rdc=true -D PROB_HEURISTIC -D AIMODE -D SEARCH_DEPTH=$search_depth 
    clang -c main.c -O3 -I $SnakeAIPath/ -I ./includes/ -I $CUDA_PATH/include/ -D AIMODE -D PROB_HEURISTIC
    nvcc *.o -o Snake -lSDL2 -lm -arch=sm_61  -lcudadevrt -O3
    rm *.o
    exit
  elif [ $1 -eq 1 ]
    then
    clang -c $SnakeAIPath/greedy_local_optimum.c -I ./includes/ -D AIMODE -O3
    clang -c main.c -I $SnakeAIPath/ -I ./includes/ -D AIMODE -O3
  elif [ $1 -eq 2 ]
    then
    clang -c *.c -I ./includes/ -D NETWORK_MODE -O3 -I/opt/homebrew/include/ -D_THREAD_SAFE -L/opt/homebrew/lib -lSDL2 -lSDL2_net
  fi
  else
    clang -c main.c  -I/opt/homebrew/include/ -D_THREAD_SAFE -L/opt/homebrew/lib -lSDL2 -O3
fi
clang *.o -o Snake -I/opt/homebrew/include/ -D_THREAD_SAFE -L/opt/homebrew/lib -lSDL2 -lSDL2_net -O3
rm *.o


