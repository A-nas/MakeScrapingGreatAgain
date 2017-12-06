<?php
    	$manager = new MongoDB\Driver\Manager("mongodb://localhost:27017");
        $query = new MongoDB\Driver\Query(array('tweetDate' => '4 nov. 2014'));
        $cursor = $manager->executeQuery('paperman.course', $query);
        print json_encode( $cursor->toArray() );
        //print_r($cursor->toArray());
?>