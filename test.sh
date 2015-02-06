$wtf = curl http://localhost:8000/EEG/login | grep -o 'value='\''[^;]*'\'''
echo $wtf 
