package test;

public class test1 {
    abstract class Instrument {
        public abstract void play();
    }

    class Wind extends Instrument {
        public void play() {
            System.out.println("弹奏Wind");
        }
    }

    class Brass extends Instrument {
        public void play() {
            System.out.println("弹奏Brass");
        }
    }

   public static class Music {
        public void tune(Instrument i) {
            i.play();
        }
    }

    public static class E {
        public static void main(String[] args) {

            Music music = new Music();
            music.tune(new Wind());
            music.tune(new Brass());

        }
    }
}
