using NUnit.Framework;
using System;
using System.Linq;
using System.IO;
using System.Net;
using System.Text.RegularExpressions;
using System.Text;

namespace MyApp.AcceptanceTests
{
    [TestFixture]
    [Parallelizable(ParallelScope.Children)]
    public class AcceptanceTests
    {
        
        private string runName;
        private string runServer;
        private string appName = "MyApp";
        private WebInject webinject;
        
        [OneTimeSetUp]
        protected void OneTimeSetUp()
        {
            runName = Dashboard.RandomString(5);
            runServer = Dashboard.RunServer();

            string ns = GetType().Namespace;

            webinject = new WebInject(ns + "_" +runName);
        }

        [SetUp]
        protected void SetUp()
        {
            // pass
        }

        [TearDown]
        protected void TearDown()
        {
            // pass
        }

        [Test]
        public void SleepyTest1()
        {
            string test = @"
step: Sleepy Test1
shell: echo retry {RETRY}
verifypositive: retry 4
sleep: 1
retry: 5
            ";

            string result = webinject.Submit(test);

            Assert.IsTrue( result.Contains("WEBINJECT TEST PASSED") , "Failed" );
        }

        [Test]
        public void SleepyTest2()
        {
            string test = @"
step: Sleepy Test2
shell: echo retry {RETRY}
verifypositive: retry 4
sleep: 1
retry: 5
            ";

            string result = webinject.Submit(test);

            Assert.IsTrue( result.Contains("WEBINJECT TEST PASSED") , "Failed" );
        }

        [Test]
        public void SleepyTest3()
        {
            string test = @"
step: Sleepy Test3
shell: echo retry {RETRY}
verifypositive: retry 4
sleep: 1
retry: 5
            ";

            string result = webinject.Submit(test);

            Assert.IsTrue( result.Contains("WEBINJECT TEST PASSED") , "Failed" );
        }

        [Test]
        public void ShellCommands()
        {
            string test = @"
step: This is step one
shell1: echo hello

step: This is step two
shell1: echo hi again
shell2: dir
            ";

            string result = webinject.Submit(test);

            Assert.IsTrue( result.Contains("WEBINJECT TEST PASSED") , "Failed" );
        }

        [Test]
        public void FailureDetected()
        {
            string test = @"
step: This is step one
shell1: echo hello
verifypositive: goodbye
            ";

            string result = webinject.Submit(test);

            Assert.IsTrue( result.Contains("WEBINJECT TEST FAILED") , "Failed to fail" );
        }

        [Test]
        public void PublicInternet()
        {
            string test = @"
step: Get Totaljobs Homepage
url: https://www.totaljobs.com
verifypositive: More options
            ";

            string result = webinject.Submit(test);

            Assert.IsTrue( result.Contains("WEBINJECT TEST PASSED") , "Failed" );
        }

        [Test]
        public void ThisServer()
        {
            string test = @"
step: Get Dash Results on this server
url: http://[THIS_SERVER]/dash/results/
verifypositive: Latest run results for all apps
            ";

            string result = webinject.Submit(test);

            Assert.IsTrue( result.Contains("WEBINJECT TEST PASSED") , "Failed" );
        }

        [Test]
        public void TargetServer()
        {
            string test = @"
step: Get Dash Results on the target server
url: http://[TARGET_SERVER]/dash/results/
verifypositive: Latest run results for all apps
            ";

            string result = webinject.Submit(test);

            Assert.IsTrue( result.Contains("WEBINJECT TEST PASSED") , "Failed" );
        }

    }

    public class WebInject
    {

        private string batch;
        
        public WebInject (string batch) {
            this.batch = batch;
        }
    
    //        static string targetServer = "[THIS_SERVER]";
        static string targetServer = "dash";
   
        static string server_uri = "http://dash/webinject/server/submit/";

        public string Submit(string test) {

            string result;

            test = SubVariables(test);

            string uri = server_uri + "?batch=" + batch;
            result = Util.Post(uri, "steps="+test);
            //Console.WriteLine(result);

            return result;
        }
        
        public static string SubVariables(string test) {
            test = test.Replace( "[TARGET_SERVER]", targetServer );
            test = test.Replace( "[THIS_SERVER]", ThisServerHost() );
            return test;
        }
        
        public static string ThisServerHost() {
            string computername = Environment.GetEnvironmentVariable("computername");
            string userdnsdomain = Environment.GetEnvironmentVariable("userdnsdomain");
            return computername+"."+userdnsdomain;
        }
    }

    public static class Dashboard
    {

        private static Random random = new Random();
        public static string RandomString(int length)
        {
            const string chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
            return new string(Enumerable.Repeat(chars, length)
              .Select(s => s[random.Next(s.Length)]).ToArray());
        }
        
        public static string RunServer()
        {
            return Environment.GetEnvironmentVariable("computername");
        }

        public static string LogResult(string testName, string appName, string runName, string runServer, string testStatus, string message)
        {
            string logURL = "http://dash/dash/results/log?";
            string queryString = String.Format("test_name={0}&app_name={1}&run_name={2}&run_server={3}&test_passed={4}&message={5}",
                                     testName, appName, runName, runServer, testStatus, message);

            try
            {
                string response = Util.Get(logURL + queryString);
                if ( !(response.Contains("Test logged ok")) ) {
                    Console.WriteLine("Error message logging test for URL: " + logURL + queryString);
                    Console.WriteLine(response);
                }
                return response;
            }
            catch (WebException e)
            {
                Console.WriteLine("Server error logging test for URL: " + logURL + queryString);
                return "Web request failed";
            }
        }

        public static string GetTestName()
        {
            return Dashboard._LastTwoSegmentsOfNUnitTestFullName(NUnit.Framework.TestContext.CurrentContext.Test.FullName);
        }

        //NUnit.Framework.TestContext.CurrentContext.Result.StackTrace
        //NUnit.Framework.TestContext.CurrentContext.Result.Outcome.Status; (For test Execution Status)

        public static string GetTestMessage()
        {
            return NUnit.Framework.TestContext.CurrentContext.Result.Message;
        }

        private static string _LastTwoSegmentsOfNUnitTestFullName(string testName)
        {
            string[] segments = Regex.Split(testName, "\\.");
            return segments[segments.Length - 2] + "." + segments.Last();
        }

        public static string GetTestStatus()
        {
            return NUnit.Framework.TestContext.CurrentContext.Result.Outcome.Status.ToString();
        }

    }
    
    public static class Util {
        public static string Get(string uri)
        {
            HttpWebRequest request = (HttpWebRequest)WebRequest.Create(uri);
            request.AutomaticDecompression = DecompressionMethods.GZip | DecompressionMethods.Deflate;

            using(HttpWebResponse response = (HttpWebResponse)request.GetResponse())
            using(Stream stream = response.GetResponseStream())
            using(StreamReader reader = new StreamReader(stream))
            {
                return reader.ReadToEnd();
            }
        }

        public static string Post(string uri, string postData)  {

            var request = (HttpWebRequest)WebRequest.Create(uri);
             
            var data = Encoding.ASCII.GetBytes(postData);
             
            request.Method = "POST";
            request.ContentType = "application/x-www-form-urlencoded";
            request.ContentLength = data.Length;
             
            using (var stream = request.GetRequestStream())
            {
                stream.Write(data, 0, data.Length);
            }
             
            var response = (HttpWebResponse)request.GetResponse();
             
            var responseString = new StreamReader(response.GetResponseStream()).ReadToEnd();

            return responseString;
        }

    }

}