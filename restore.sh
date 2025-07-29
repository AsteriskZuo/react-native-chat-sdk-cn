set -e
set -u

target_dir="/Users/asterisk/Codes/zuoyu/react-native-chat-sdk-cn"
source_dir="/Users/asterisk/Codes/rn/react-native-chat-sdk-rn72"

cp -p -R -f ${source_dir}/src ${target_dir}
cp -p -R -f ${source_dir}/docs ${target_dir}
cp -p -R -f ${source_dir}/scripts ${target_dir}