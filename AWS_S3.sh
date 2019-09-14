#!/bin/bash

AWS_BUCKET=www.mybacketsample.net
KEY_FILE=jre-8u201-macosx-x64.dmg

split -b 5m ${KEY_FILE} splitFile

Tag_Upload_Id=`aws s3api create-multipart-upload --bucket ${AWS_BUCKET} --key ${KEY_FILE}|grep "UploadId"`
Upload_Id=`echo ${Tag_Upload_Id} | cut -f 2 -d":" | xargs`
echo $Upload_Id
Upload_Id=`echo ${Upload_Id}|sed 's/^.*"\(.*\)".*$/\1/'`

File_Part=1
File_Num=`ls -1 splitFile* | wc -l`
ETag_List=()

#JSON作成
echo -e "{\n    \"Parts\": [" > fileparts.json

for File_Name in `ls -1 splitFile*`; do
   echo "File_Name:${File_Name}"
   echo "File_Part:${File_Part}"
    
   Send_File_MD5=`openssl md5 -binary ${File_Name} | base64`
   
   echo "Send_File_MD5:${Send_File_MD5}"
   
   ETag_DQ_C=`aws s3api upload-part --bucket "${AWS_BUCKET}" --key "${KEY_FILE}" --part-number ${File_Part} --body "${File_Name}" --upload-id ${Upload_Id}  --content-md5 ${Send_File_MD5} |grep "ETag"`
   
   echo "EDIT TARGET: ${ETag_DQ_C}"
   ETag_DQ=`echo ${ETag_DQ_C}|sed s/,//g`
   ETag_DQ=`echo "${ETag_DQ}"| cut -f 2 -d":"`
   ETag=`echo ${ETag_DQ} | sed "s/[\"][\\]//" | sed "s/[\\][\"]//"`
   echo "EDIT AFTER :${ETag}"
   
   echo "    {" >>  fileparts.json
   echo "        \"ETag\": ${ETag}," >> fileparts.json
   echo "        \"PartNumber\":${File_Part}" >> fileparts.json

   if [ ${File_Num} -eq ${File_Part} ]; then
       echo "    }]" >> fileparts.json
   else
       echo "    }," >> fileparts.json
   fi

   File_Part=$(( File_Part + 1 ))
done
echo "}" >> fileparts.json

aws s3api list-parts --bucket ${AWS_BUCKET} --key ${KEY_FILE} --upload-id ${Upload_Id}
aws s3api complete-multipart-upload --multipart-upload file://fileparts.json --bucket "${AWS_BUCKET}" --key "${KEY_FILE}"  --upload-id ${Upload_Id}

rm ./splitFile*
rm ./fileparts.json
