while true; do
    curl -o "$1/$(date +%s).jpg" "$2"
    sleep 1
done
