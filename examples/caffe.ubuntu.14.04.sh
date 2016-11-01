sudo apt-get install libprotobuf-dev libleveldb-dev libsnappy-dev libopencv-dev libhdf5-serial-dev protobuf-compiler
sudo apt-get install --no-install-recommends libboost-all-dev
sudo apt-get install libgflags-dev libgoogle-glog-dev liblmdb-dev
git clone https://github.com/BVLC/caffe.git
cd caffe
cp Makefile.config.example Makefile.config
make all
make test
make runtest
