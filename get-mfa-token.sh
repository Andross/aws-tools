#!/bin/bash

set_shell_env() {
    OUTPUT=$(aws sts get-session-token --serial-number $1 --profile $2 --token-code $3 )
  
    accesskeyid=$(echo $OUTPUT | jq -r '.Credentials'|jq -r '.AccessKeyId')
    export AWS_ACCESS_KEY_ID=$accesskeyid

    secretkey=$(echo $OUTPUT | jq -r '.Credentials'|jq -r '.SecretAccessKey')
    export AWS_SECRET_ACCESS_KEY=$secretkey

    sessiontoken=$(echo $OUTPUT | jq -r '.Credentials'|jq -r '.SessionToken')
    export AWS_SESSION_TOKEN=$sessiontoken    
}

set_shell_env "$1" "$2" "$3"