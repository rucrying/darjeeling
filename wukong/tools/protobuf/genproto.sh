WUKONG_HOME=/Users/Peter/PhpstormProjects/wukong-darjeeling/wukong
PROTO_HOME=/Users/Peter/Documents/install/protobuf-2.6.0/src
SERVICE_PATH=$WUKONG_HOME/master/service

cd $PROTO_HOME
sh protoc --proto_path=$SERVICE_PATH/proto --python_out=$SERVICE_PATH/storage/model  $SERVICE_PATH/proto/storage.proto
sh protoc --proto_path=$SERVICE_PATH/proto --python_out=$SERVICE_PATH/configure/model  $SERVICE_PATH/proto/configure.proto