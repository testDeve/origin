#!/bin/bash

Upload_Id_List=()
Key_List=()

for Upload_Id in `aws s3api list-multipart-uploads --bucket www.mybacketsample.net|grep UploadId`; do
    if [ ! ${Upload_Id:0:10} = \"UploadId\" ]; then
       Upload_Id_DQ=`echo ${Upload_Id}| sed s/,//g`
       Upload_Id=`echo ${Upload_Id_DQ}|sed 's/^.*"\(.*\)".*$/\1/'`
       Upload_Id_List+=(`echo ${Upload_Id}`)
    fi
done

for Key in `aws s3api list-multipart-uploads --bucket www.mybacketsample.net|grep Key`; do
    if [ ! ${Key:0:5} = \"Key\" ]; then
       Key_DQ=`echo ${Key}| sed s/,//g`
       Key=`echo ${Key_DQ}|sed 's/^.*"\(.*\)".*$/\1/'`
       Key_List+=(`echo ${Key}`)
    fi
done

count=`expr ${#Upload_Id_List[@]} - 1`

if [ ${count} -eq "-1" ]; then
  echo "abort-multipart-upload Not Found !!"
  exit 1
fi

for index in `seq 0 ${count}`; do
  sleep 1
  aws s3api abort-multipart-upload --bucket www.mybacketsample.net --key ${Key_List[${index}]} --upload-id ${Upload_Id_List[$index]}
  if [ $? -eq 0 ]; then
    echo "abort-multipart-upload Delete Complete !! Key:${Key_List[${index}]} UploadId:${Upload_Id_List[$index]}"
  fi
done
