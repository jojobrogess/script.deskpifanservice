cd ~/
wget https://github.com/jojobrogess/pyserial/archive/refs/tags/v3.5.tar.gz -O pyserial-3.5.tar.gz 
export tmp_dir=~/install_temp/
mkdir $tmp_dir
cd $tmp_dir
tar -xvf ~/pyserial*.tar.gz
cd pyserial*
python setup.py install --user 
cd ~/
rm $tmp_dir/ -Rf
rm pyserial-3.5.tar.gz
