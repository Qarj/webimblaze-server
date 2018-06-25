 #!/usr/bin/perl
 {
 package MyWebServer;
 
 use HTTP::Server::Simple::CGI;
 use Net::Server::PreFork;
# use base qw(HTTP::Server::Simple::CGI);

 use base qw(Net::Server::PreFork); # any personality will do
 
 my %dispatch = (
     '/hello' => \&resp_hello,
     '/wif' => \&resp_wif,
     # ...
 );
 
 sub handle_request {
     my $self = shift;
     my $cgi  = shift;
   
     my $path = $cgi->path_info();
     my $handler = $dispatch{$path};
 
     if (ref($handler) eq "CODE") {
         print "HTTP/1.0 200 OK\r\n";
         $handler->($cgi);
         
     } else {
         print "HTTP/1.0 404 Not found\r\n";
         print $cgi->header,
               $cgi->start_html('Not found'),
               $cgi->h1('Not found'),
               $cgi->end_html;
     }
 }
 
 sub resp_hello {
     # http://localhost:8080/hello?name=MyName
     my $cgi  = shift;   # CGI.pm object
     return if !ref $cgi;
     
     my $who = $cgi->param('name');

     my ( $yyyy, $mm, $dd, $hour, $minute, $second, $seconds ) = get_date(0); ## no critic(NamingConventions::ProhibitAmbiguousNames)
     my $_time_1 = "$hour:$minute:$second";

     sleep 7;

     ( $yyyy, $mm, $dd, $hour, $minute, $second, $seconds ) = get_date(0); ## no critic(NamingConventions::ProhibitAmbiguousNames)
     my $_time_2 = "$hour:$minute:$second";
     
     print $cgi->header,
           $cgi->start_html("Hello"),
           $cgi->h1("Hello $who!"),
           $cgi->h2("Start $_time_1"),
           $cgi->h2("Stop $_time_2"),
           $cgi->end_html;
 }
 
sub resp_wif {
    # http://localhost:8080/wif?test=get
    my $cgi  = shift;   # CGI.pm object
    return if !ref $cgi;
    
    #my $_pid = fork;
    #if ($_pid) {
    #    # parent process should return and listen for requests
    #    return;
    #}

    my $_testfile_name = $cgi->param('test');

    my $_result = `wif.pl $_testfile_name`;
    
    print $cgi->header,
          $cgi->start_html("results"),
          $cgi->h1("Execution results for $_testfile_name!"),
          "<xmp>$_result</xmp>",          
          $cgi->end_html;

    #exit;
}

#------------------------------------------------------------------
sub get_date {
    my ($_time_offset) = @_;

    ## put the specified date and time into variables - startdatetime - for recording the start time in a format an xsl stylesheet can process
    my @_MONTHS = qw(01 02 03 04 05 06 07 08 09 10 11 12);
    #my @_WEEKDAYS = qw(Sun Mon Tue Wed Thu Fri Sat Sun);
    my ($_SECOND, $_MINUTE, $_HOUR, $_DAYOFMONTH, $_MONTH, $_YEAROFFSET, $_DAYOFWEEK, $_DAYOFYEAR, $_DAYLIGHTSAVINGS) = localtime (time + $_time_offset);
    my $_YEAR = 1900 + $_YEAROFFSET;
    #my $_YY = substr $_YEAR, 2; #year as 2 digits
    $_DAYOFMONTH = sprintf '%02d', $_DAYOFMONTH;
    #my $_WEEKOFMONTH = int(($_DAYOFMONTH-1)/7)+1;
    $_MINUTE = sprintf '%02d', $_MINUTE; #put in up to 2 leading zeros
    $_SECOND = sprintf '%02d', $_SECOND;
    $_HOUR = sprintf '%02d', $_HOUR;
    my $_TIMESECONDS = ($_HOUR * 60 * 60) + ($_MINUTE * 60) + $_SECOND;

    return $_YEAR, $_MONTHS[$_MONTH], $_DAYOFMONTH, $_HOUR, $_MINUTE, $_SECOND, $_TIMESECONDS;
}


} 
 
# start the server on port 8080
#my $pid = MyWebServer->new(8080)->background();
my $pid = MyWebServer->run(port => 8080, ipv => '*');
print "Use 'kill $pid' to stop server.\n";