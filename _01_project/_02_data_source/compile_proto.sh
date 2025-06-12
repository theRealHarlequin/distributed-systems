#!/bin/bash

for f in $(ls *.proto); do
    "C:\work\study\lab_verteilte_Systme\protoc\bin\protoc.exe" --proto_path=. ./$f --python_out=.
done

sleep 5