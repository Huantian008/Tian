package legacy.oop.test;

public class test1 {
    private interface Instrument {
        void play();
    }

    private static final class Wind implements Instrument {
        @Override
        public void play() {
            System.out.println("Playing Wind");
        }
    }

    private static final class Brass implements Instrument {
        @Override
        public void play() {
            System.out.println("Playing Brass");
        }
    }

    private static final class Music {
        public void tune(Instrument instrument) {
            instrument.play();
        }
    }

    public static void main(String[] args) {
        Music music = new Music();
        music.tune(new Wind());
        music.tune(new Brass());
    }
}
