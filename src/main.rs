use std::time::Duration;
use std::str;
use serialport;

const port: &str = "/dev/ttyS0";

fn main() {
    let mut s = serialport::new(port, 9600)
        .timeout(Duration::from_millis(10))
        .open().expect("failed to open port");


    let mut buff = [0; 2];
    let mut line = String::new();
    let mut index = 0;
    loop {
        if let Ok(n) = s.read(&mut buff) {
            let b = &buff[0..n];
            if !b.is_ascii() {
                continue
            }

            if b.len() == 1 && b[0] == 3 {
                break
            } else if b.len() == 1 && b[0] == 2 {
                index += 1;
                continue
            }

            if index == 11 {
                break;
            }

            let r = String::from_iter(b.to_ascii_lowercase().iter().map(|v| { *v as char }));
            println!("{:?} {:?}", b, r);
            line += &r;
            index += 1;
        }
    }

    println!("{}", line);
}
