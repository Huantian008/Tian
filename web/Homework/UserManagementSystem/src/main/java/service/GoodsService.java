package service;

import dao.GoodsDao;
import model.Goods;

import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

public class GoodsService {
    private GoodsDao gDao = new GoodsDao();

    public List<Goods> getGoodsList(int recommendType) {
        try {
            List<Goods> list = gDao.getGoodsList(recommendType);
            if (list.isEmpty()) {
                return gDao.selectGoodsByTypeID(0, 1, 8);
            }
            return list;
        } catch (SQLException e) {
            e.printStackTrace();
            return new ArrayList<Goods>();
        }
    }

    public List<Goods> getGoodsList(int typeId, int pageNumber, int pageSize) {
        try {
            return gDao.selectGoodsByTypeID(typeId, pageNumber, pageSize);
        } catch (SQLException e) {
            e.printStackTrace();
            return new ArrayList<Goods>();
        }
    }

    public Goods getScrollGood() {
        try {
            return gDao.getScrollGood();
        } catch (SQLException e) {
            e.printStackTrace();
            return null;
        }
    }

    public Goods getGoodsById(int id) {
        try {
            return gDao.getGoodsById(id);
        } catch (SQLException e) {
            e.printStackTrace();
            return null;
        }
    }

    public int getSearchCount(String keyword) {
        try {
            return gDao.getSearchCount(keyword);
        } catch (SQLException e) {
            e.printStackTrace();
            return 0;
        }
    }

    public List<Goods> selectSearchGoods(String keyword, int pageNumber, int pageSize) {
        try {
            return gDao.selectSearchGoods(keyword, pageNumber, pageSize);
        } catch (SQLException e) {
            e.printStackTrace();
            return new ArrayList<Goods>();
        }
    }

    public void addRecommend(int id, int type) {
        try {
            gDao.addRecommend(id, type);
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public void removeRecommend(int id, int type) {
        try {
            gDao.removeRecommend(id, type);
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public void insert(Goods goods) {
        try {
            gDao.insert(goods);
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public void update(Goods goods) {
        try {
            gDao.update(goods);
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public void delete(int id) {
        try {
            gDao.delete(id);
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
