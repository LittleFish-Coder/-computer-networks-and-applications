echo '1'
python3 ./client.py 12000 example.com. A 5
echo '2'
python3 ./client.py 12000 example.org. A 1
echo '3'
python3 ./client.py 12000 bar.example.com. CNAME 5
echo '4'
python3 ./client.py 12000 . NS 5
echo '5'
python3 ./client.py 12000 bar.example.com. A 5
echo '6'
python3 ./client.py 12000 foo.example.com. A 5
echo '7'
python3 ./client.py 12000 example.org. A 5
echo '8'
python3 ./client.py 12000 example.org. CNAME 5
echo '9'
python3 ./client.py 12000 example.org. NS 5
echo '10'
python3 ./client.py 12000 www.metalhead.com. A 5
