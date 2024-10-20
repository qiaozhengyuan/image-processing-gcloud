curl -X POST http://127.0.0.1:8080 \
    -F "file=@/mnt/c/Users/qiaoz/OneDrive/桌面/Interview/Mandai/test.png"
curl -G "http://127.0.0.1:8080" \
     --data-urlencode "image_id=6d648d4d-1b78-4522-8c88-0f8bc22d73aa" \
     --data-urlencode "format=png" \
     -o retrieval.png
curl -G "http://127.0.0.1:8080" \
     --data-urlencode "image_id=6d648d4d-1b78-4522-8c88-0f8bc22d73aa" \
     --data-urlencode "format=jpeg" \
     -o retrieval.jpg
