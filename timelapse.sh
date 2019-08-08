while true; do
    FILE_NAME="$1/$(date +%s).jpg"
    URL=$2
    curl -o $FILE_NAME $URL
    echo $FILE_NAME
    sleep 1
done
