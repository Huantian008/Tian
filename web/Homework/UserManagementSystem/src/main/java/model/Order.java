package model;

import utils.PriceUtils;

import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Order {
    private int id;
    private float total;
    private int amount;
    private int status;
    private int paytype;
    private String name;
    private String phone;
    private String address;
    private Date datetime;
    private User user;
    private Map<Integer, OrderItem> itemMap = new HashMap<Integer, OrderItem>();
    private List<OrderItem> itemList = new ArrayList<OrderItem>();

    public Order() {
    }

    public Order(int id, float total, int amount, int status, int paytype, String name,
                 String phone, String address, Date datetime, User user) {
        this.id = id;
        this.total = total;
        this.amount = amount;
        this.status = status;
        this.paytype = paytype;
        this.name = name;
        this.phone = phone;
        this.address = address;
        this.datetime = datetime;
        this.user = user;
    }

    public void addGoods(Goods goods) {
        if (goods == null) {
            return;
        }
        OrderItem item = itemMap.get(goods.getId());
        if (item == null) {
            item = new OrderItem(goods.getPrice(), 1, goods, this);
            itemMap.put(goods.getId(), item);
        } else {
            item.setAmount(item.getAmount() + 1);
        }
        rebuildItems();
        amount++;
        total = PriceUtils.add(total, goods.getPrice());
    }

    public void less(int goodsid) {
        OrderItem item = itemMap.get(goodsid);
        if (item == null) {
            return;
        }
        item.setAmount(item.getAmount() - 1);
        amount--;
        total = PriceUtils.subtract(total, item.getPrice());
        if (item.getAmount() <= 0) {
            itemMap.remove(goodsid);
        }
        normalizeTotals();
        rebuildItems();
    }

    public void delete(int goodsid) {
        OrderItem item = itemMap.get(goodsid);
        if (item == null) {
            return;
        }
        amount -= item.getAmount();
        total = PriceUtils.subtract(total, item.getAmount() * item.getPrice());
        itemMap.remove(goodsid);
        normalizeTotals();
        rebuildItems();
    }

    private void rebuildItems() {
        itemList = new ArrayList<OrderItem>(itemMap.values());
    }

    private void normalizeTotals() {
        if (amount < 0) {
            amount = 0;
        }
        if (total < 0.0001f) {
            total = 0.0f;
        }
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public float getTotal() {
        return total;
    }

    public void setTotal(float total) {
        this.total = total;
    }

    public int getAmount() {
        return amount;
    }

    public void setAmount(int amount) {
        this.amount = amount;
    }

    public int getStatus() {
        return status;
    }

    public void setStatus(int status) {
        this.status = status;
    }

    public int getPaytype() {
        return paytype;
    }

    public void setPaytype(int paytype) {
        this.paytype = paytype;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getPhone() {
        return phone;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public Date getDatetime() {
        return datetime;
    }

    public void setDatetime(Date datetime) {
        this.datetime = datetime;
    }

    public User getUser() {
        return user;
    }

    public void setUser(User user) {
        this.user = user;
    }

    public Map<Integer, OrderItem> getItemMap() {
        return itemMap;
    }

    public void setItemMap(Map<Integer, OrderItem> itemMap) {
        this.itemMap = itemMap;
        rebuildItems();
    }

    public List<OrderItem> getItemList() {
        return itemList;
    }

    public void setItemList(List<OrderItem> itemList) {
        this.itemList = itemList;
    }
}
