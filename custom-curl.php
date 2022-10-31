<?php


require_once('token.php');

function curl_setopt_custom_postfields($ch, $postfields, $headers = null) {
    global $JIRA_TOKEN;
    $algos = hash_algos();
    $hashAlgo = null;
    foreach ( array('sha1', 'md5') as $preferred ) {
        if ( in_array($preferred, $algos) ) {
            $hashAlgo = $preferred;
            break;
        }
    }
    if ( $hashAlgo === null ) { list($hashAlgo) = $algos; }
    $boundary =
        '----------------------------' .
        substr(hash($hashAlgo, 'rHxZU0XwipAtusCzp3F0Hve2SaGPnPSBg9CxR8GQ' . microtime()), 0, 12);

    $body = array();
    $crlf = "\r\n";
    $fields = array();
    foreach ( $postfields as $key => $value ) {
        if ( is_array($value) ) {
            foreach ( $value as $v ) {
                $fields[] = array($key, $v);
            }
        } 
        else {
            $fields[] = array($key, $value);
        }
    }


    foreach ( $fields as $field ) {
        list($key, $value) = $field;
        if ( strpos($value, '@') === 0 ) {
            preg_match('/^@(.*?)$/', $value, $matches);
            list($dummy, $filename) = $matches;
            $body[] = '--' . $boundary;
            $body[] = 'Content-Disposition: form-data; name="' . $key . '"; filename="' . basename($filename) . '"';
            $body[] = 'Content-Type: application/octet-stream';
            $body[] = '';
            $body[] = file_get_contents($filename);
        } 
        else {
            $body[] = '--' . $boundary;
            $body[] = 'Content-Disposition: form-data; name="' . $key . '"';
            $body[] = '';
            $body[] = $value;
        }
    }

    $body[] = '--' . $boundary . '--';
    $body[] = '';
    $contentType = 'multipart/form-data; boundary=' . $boundary;
    $content = join($crlf, $body);
    $contentLength = strlen($content);

    //var_dump($content);

    curl_setopt($ch, CURLOPT_HTTPHEADER, array(
        'Content-Length: ' . $contentLength,
        'Expect: 100-continue',
        'Content-Type: ' . $contentType,
        'User-Agent: curl',
        //'Accept-Encoding: gzip, deflate',
        'Accept: application/json',
        'Connection: keep-alive',
        'X-Atlassian-Token: no-check',
        'X-ExperimentalApi: opt-in',
        'Authorization: Bearer ' . $JIRA_TOKEN,
    ));

    curl_setopt($ch, CURLOPT_POSTFIELDS, $content);

}


/************** Usage *******************/
$BASE = 'https://jira-epic.woc.noaa.gov';
$url = "{$BASE}/rest/servicedeskapi/servicedesk/1/attachTemporaryFile";
//$url = 'http://localhost:8000';
//$url = 'httpbin.org/anything';
//$url = 'httpbin.org/post';
//$url = 'http://localhost:8000';
$crl = curl_init($url);
curl_setopt($crl, CURLOPT_RETURNTRANSFER, true);
curl_setopt($crl, CURLINFO_HEADER_OUT, true);
curl_setopt($crl, CURLOPT_POST, true);

$postfields = [
    'file' => array('@a.txt', '@a.html', '@a.bin'),
    //'file' => [ ['@a.txt', 'text/plain'], ['@a.html', 'text/html'], ['@a.bin', 'application/octet-stream']];
    //'name' => array('James', 'Peter', 'Richard'),
];

curl_setopt_custom_postfields($crl, $postfields);

$result = curl_exec($crl);

echo "================================================================\n\n";
var_dump($result);
echo "================================================================\n\n";




