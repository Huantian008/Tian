package model;

public class OrderItem {
    private int id;
    private float price;
    private int amount;
    private String goodsName;
    private Goods goods;
    private Order order;

    public OrderItem() {
    }

    public OrderItem(float price, int amount, Goods goods, Order order) {
        this.price = price;
        this.amount = amount;
        this.goods = goods;
        this.order = order;
        this.goodsName = goods == null ? null : goods.getName();
    }

    public OrderItem(int id, float price, int amount, Goods goods, Order order) {
        this.id = id;
        this.price = price;
        this.amount = amount;
        this.goods = goods;
        this.order = order;
        this.goodsName = goods == null ? null : goods.getName();
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public float getPrice() {
        return price;
    }

    public void setPrice(float price) {
        this.price = price;
    }

    public int getAmount() {
        return amount;
    }

    public void setAmount(int amount) {
        this.amount = amount;
    }

    public String getGoodsName() {
        return goodsName;
    }

    public void setGoodsName(String goodsName) {
        this.goodsName = goodsName;
    }

    public Goods getGoods() {
        return goods;
    }

    public void setGoods(Goods goods) {
        this.goods = goods;
        this.goodsName = goods == null ? null : goods.getName();
    }

    public Order getOrder() {
        return order;
    }

    public void setOrder(Order order) {
        this.order = order;
    }
}
