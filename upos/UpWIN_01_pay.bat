@echo off
set /p sum=Please, input sum of pay in coins (for example: 105 = 1.05): 
echo 933 - BYN
echo 840 - USD
echo 978 - EUR
echo 643 - RUR
echo 974 - BYR
set /p cur=Please, choose currency of pay (for example: 840): 
start UpWin.exe 1 %sum% /r=%cur%