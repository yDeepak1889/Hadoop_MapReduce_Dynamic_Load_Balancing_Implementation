import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.fs.FSDataInputStream;
import java.io.BufferedInputStream;
import java.io.FileInputStream;
import java.io.InputStream;
import java.io.OutputStream;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.FileStatus;
import org.apache.hadoop.fs.BlockLocation;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IOUtils;
import org.apache.hadoop.util.ToolRunner;
import java.io.*;
import java.util.*;


public class HDFSClientTesting extends Configured implements Tool {

	public static final String FS_PARAM_NAME = "fs.defaultFS";
    
    public int run(String[] args) throws Exception {
       
	Configuration conf = getConf();

	System.out.println("configured filesystem = " + conf.get(FS_PARAM_NAME));

	FileSystem fs = FileSystem.get(conf);

	Path dataset = new Path(fs.getHomeDirectory(), "books/alice.txt");

	if (!fs.exists(dataset)) {
		System.err.println("output path doesn't exist");
		return 1;
	}

	FSDataInputStream in = fs.open(dataset);
	int len = in.available();
	System.out.println("-----"+ len);
    	
	byte [] out = new byte[len];
	
	int numBytes;

    	in.readFully(170000, out, 0, len-170000);
	/*
	String temp;	

	 while ((numBytes = in.read(out)) > 0) {
		temp = new String (out, "UTF-8");
		System.out.println(temp);	                
         }

	*/
	String outputStr = new String (out, "UTF-8");
    	System.out.println(outputStr);
    	out = null;
	fs.close();
	
    	return 0;
    }

	public static void main( String[] args ) throws Exception {
	        int returnCode = ToolRunner.run(new HDFSClientTesting(), args);
	        System.exit(returnCode);
	}
}
