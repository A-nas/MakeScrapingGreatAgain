<?php
    	/*$manager = new MongoDB\Driver\Manager("mongodb://localhost:27017");
        $query = new MongoDB\Driver\Query(array('tweetDate' => '4 nov. 2014'));
        $cursor = $manager->executeQuery('paperman.course', $query);
        print json_encode( $cursor->toArray() );*/
        //print_r($cursor->toArray());

        // #1
        $manager = new \MongoDB\Driver\Manager("mongodb://localhost:27017");
        $command = new \MongoDB\Driver\Command([
                'aggregate' => 'yay',
                'pipeline' => [
                    ['$project' => 
                        [
                         'tweet' => '$teweet',
                         'month' => ['$month' => '$tweetDate'],
                         'year' => ['$year' => '$tweetDate'],
                         //['monthNyear' => [ '$concat' => ['$month', ' ' , '$year' ]]] 
                        ]  
                    ],
                    ['$group' => ['_id' => ['Day' => '$month']],
                    ['$sort' => [ 'Day' => -1 ] ],
                ]],
                'cursor' => new \stdClass,]);
        $cursor = $manager->executeCommand('paperman', $command);
        echo json_encode( $cursor->toArray());

        //print_r(json_encode( $cursor->toArray() ));
            //return new JsonResponse( json_encode( $cursor->toArray() ) );


?>