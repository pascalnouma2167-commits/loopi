<?php
declare(strict_types=1);require __DIR__.'/app/bootstrap.php';header('Content-Type: text/plain; charset=utf-8');$base=rtrim((string)cfg('app.base_url'),'/' );echo "User-agent: *\nAllow: /\nDisallow: /admin/\nDisallow: /api/\n";if($base!=='')echo 'Sitemap: '.$base."/sitemap.xml\n";
