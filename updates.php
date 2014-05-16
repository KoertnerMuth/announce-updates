<?php
date_default_timezone_set('Europe/Berlin');
$_PATH = 'Support/RawBin/';
$_HTMLFILE_DE = 'Contents/GLBW.html';
$_HTMLFILE_EN = 'Contents/ELBW.html';
$_RSSFILE_DE = 'de.rss';
$_RSSFILE_EN = 'en.rss';

function getFiles($path) {
	$files = scandir($path);
	for($i=0;$i< count($files); $i++) {
		if(substr($i,-4) != '.txt') unset($files[$i]);
	}
	$files = array_values($files);
	return $files;
}

function getFileContents($path,$file) {
	$file = file($path.$file);
	$a = [];
	for($i = 0; $i < count($file); $i++) {
		$line = substr($file[$i], 0, -1); 
		if($line) array_push($a, $line);
	 }
	return $a;
}

function writeHTML($file,$lang,$path,$source) {
	$doc = new DOMDocument();
	// we want a nicely formatted output
	$doc->formatOutput = true;
	libxml_use_internal_errors(true); //php thinks HTML5 DOM Elements are errors
	$doc->loadHTMLFile($file);
	libxml_clear_errors();
	

	$content = $doc->createDocumentFragment();
	switch ($lang) {
		case 'de':
			$content->appendXML('
								<footer>
									<time datetime="'.date('Y-m-d',stat($path.$source)['mtime']).'">'.date('d.m.Y',stat($path.$source)['mtime']).'</time>
								</footer>
								<header>
									<h1>Aktuelle LOCKBASE Version: '.substr($source, 0, 5).'</h1>
								</header>
								<p>Die aktuelle LOCKBASE Version '.substr($source, 0, 5).' steht ab jetzt für Sie zum Update bereit. <span class="more"><a href="@NAVI=GSupport">mehr</a></span></p>
			');
			break;
		default:
			$content->appendXML('
								<footer>
									<time datetime="'.date('Y-m-d',stat($path.$source)['mtime']).'">'.date('d.m.Y',stat($path.$source)['mtime']).'</time>
								</footer>
								<header>
									<h1>Latest LOCKBASE version:  '.substr($source, 0, 5).'</h1>
								</header>
								<p>The latest LOCKBASE version is '.substr($source, 0, 5).' and can be downloaded  <span class="more"><a href="@NAVI=GSupport">here</a></span></p>
			');
			break;
	}


	$newArticle = $doc->createElement('article', '');
	$newArticle->setAttribute('id','version');
	$newArticle->appendChild($content);

	$version = $doc->getElementById('version');

	$doc->getElementById('news')->replaceChild($newArticle, $version);

	file_put_contents($file, $doc->saveHTML());
}

function writeRSS($file,$lang,$path,$source) {
	//TODO

}

function markFileAsProcessed($path,$file) {
	$fileNew = substr($file, 0, -3);
	$fileNew = $fileNew.'bak';
	rename ($path.$file, $path.$fileNew);
}

foreach (getFiles($_PATH) as $file) {
	getFileContents($_PATH,$file);
	writeHTML($_HTMLFILE_DE,'de',$_PATH,$file);
	writeHTML($_HTMLFILE_EN,'en',$_PATH,$file);
	//writeRSS($_RSSFILE_DE,'de',$_PATH,$file);
	markFileAsProcessed($_PATH,$file);
}
?>
