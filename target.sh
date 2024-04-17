set -e
set -u

source_dir="/Users/asterisk/Codes/zuoyu/react-native-chat-sdk-cn"
target_dir="/Users/asterisk/Codes/rn/react-native-chat-sdk"

cp -p -R -f ${source_dir}/src ${target_dir}
