package javawork;

public class E {
    public static void main(String[] args) {
        Music music = new Music();
        music.tune(new Wind());
        music.tune(new Brass());
    }
}

abstract class Instrument {
    public abstract void play();
}

final class Wind extends Instrument {
    @Override
    public void play() {
        System.out.println("Playing a wind instrument");
    }
}

final class Brass extends Instrument {
    @Override
    public void play() {
        System.out.println("Playing a brass instrument");
    }
}

final class Music {
    public void tune(Instrument instrument) {
        instrument.play();
    }
}
