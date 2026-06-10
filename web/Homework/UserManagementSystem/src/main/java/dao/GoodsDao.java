package dao;

import model.Goods;
import org.apache.commons.dbutils.QueryRunner;
import org.apache.commons.dbutils.handlers.BeanHandler;
import org.apache.commons.dbutils.handlers.BeanListHandler;
import org.apache.commons.dbutils.handlers.ScalarHandler;
import utils.JDBCUtils;

import java.sql.SQLException;
import java.util.List;

public class GoodsDao {
    private static final String GOODS_COLUMNS =
            "g.id,g.name,g.cover,g.image1,g.image2,g.price,g.intro,g.stock,"
                    + "g.type_id typeid,t.name typename";

    public List<Goods> getGoodsList(int recommendType) throws SQLException {
        return selectGoodsbyRecommend(recommendType, 1, 8);
    }

    public Goods getScrollGood() throws SQLException {
        List<Goods> list = selectGoodsbyRecommend(1, 1, 1);
        if (list.isEmpty()) {
            list = selectGoodsByTypeID(0, 1, 1);
        }
        return list.isEmpty() ? null : list.get(0);
    }

    public List<Goods> selectGoodsByTypeID(int typeID, int pageNumber, int pageSize) throws SQLException {
        QueryRunner r = new QueryRunner(JDBCUtils.getDataSource());
        int offset = normalizeOffset(pageNumber, pageSize);
        if (typeID == 0) {
            String sql = "select " + GOODS_COLUMNS
                    + " from goods g left join type t on g.type_id=t.id order by g.id limit ?,?";
            return r.query(sql, new BeanListHandler<Goods>(Goods.class), offset, pageSize);
        }
        String sql = "select " + GOODS_COLUMNS
                + " from goods g left join type t on g.type_id=t.id where g.type_id=? order by g.id limit ?,?";
        return r.query(sql, new BeanListHandler<Goods>(Goods.class), typeID, offset, pageSize);
    }

    public int getCountOfGoodsByTypeID(int typeID) throws SQLException {
        QueryRunner r = new QueryRunner(JDBCUtils.getDataSource());
        if (typeID == 0) {
            String sql = "select count(*) from goods";
            Number count = r.query(sql, new ScalarHandler<Number>());
            return count.intValue();
        }
        String sql = "select count(*) from goods where type_id=?";
        Number count = r.query(sql, new ScalarHandler<Number>(), typeID);
        return count.intValue();
    }

    public List<Goods> selectGoodsbyRecommend(int type, int pageNumber, int pageSize) throws SQLException {
        QueryRunner r = new QueryRunner(JDBCUtils.getDataSource());
        int offset = normalizeOffset(pageNumber, pageSize);
        String sql = "select " + GOODS_COLUMNS
                + " from recommend r join goods g on r.goods_id=g.id"
                + " left join type t on g.type_id=t.id where r.type=? order by r.id limit ?,?";
        return r.query(sql, new BeanListHandler<Goods>(Goods.class), type, offset, pageSize);
    }

    public int getRecommendCountOfGoodsByTypeID(int type) throws SQLException {
        QueryRunner r = new QueryRunner(JDBCUtils.getDataSource());
        String sql = "select count(*) from recommend where type=?";
        Number count = r.query(sql, new ScalarHandler<Number>(), type);
        return count.intValue();
    }

    public Goods getGoodsById(int id) throws SQLException {
        QueryRunner r = new QueryRunner(JDBCUtils.getDataSource());
        String sql = "select " + GOODS_COLUMNS
                + " from goods g left join type t on g.type_id=t.id where g.id=?";
        return r.query(sql, new BeanHandler<Goods>(Goods.class), id);
    }

    public int getSearchCount(String keyword) throws SQLException {
        QueryRunner r = new QueryRunner(JDBCUtils.getDataSource());
        String sql = "select count(*) from goods where name like ?";
        Number count = r.query(sql, new ScalarHandler<Number>(), "%" + keyword + "%");
        return count.intValue();
    }

    public List<Goods> selectSearchGoods(String keyword, int pageNumber, int pageSize) throws SQLException {
        QueryRunner r = new QueryRunner(JDBCUtils.getDataSource());
        int offset = normalizeOffset(pageNumber, pageSize);
        String sql = "select " + GOODS_COLUMNS
                + " from goods g left join type t on g.type_id=t.id where g.name like ? order by g.id limit ?,?";
        return r.query(sql, new BeanListHandler<Goods>(Goods.class), "%" + keyword + "%", offset, pageSize);
    }

    public boolean isRecommend(Goods goods, int type) throws SQLException {
        if (goods == null) {
            return false;
        }
        QueryRunner r = new QueryRunner(JDBCUtils.getDataSource());
        String sql = "select count(*) from recommend where goods_id=? and type=?";
        Number count = r.query(sql, new ScalarHandler<Number>(), goods.getId(), type);
        return count.intValue() > 0;
    }

    public void addRecommend(int id, int type) throws SQLException {
        QueryRunner r = new QueryRunner(JDBCUtils.getDataSource());
        String sql = "insert into recommend(type,goods_id) select ?,? from dual where not exists "
                + "(select 1 from recommend where type=? and goods_id=?)";
        r.update(sql, type, id, type, id);
    }

    public void removeRecommend(int id, int type) throws SQLException {
        QueryRunner r = new QueryRunner(JDBCUtils.getDataSource());
        String sql = "delete from recommend where goods_id=? and type=?";
        r.update(sql, id, type);
    }

    public void insert(Goods goods) throws SQLException {
        QueryRunner r = new QueryRunner(JDBCUtils.getDataSource());
        String sql = "insert into goods(name,cover,image1,image2,price,intro,stock,type_id) values(?,?,?,?,?,?,?,?)";
        r.update(sql, goods.getName(), goods.getCover(), goods.getImage1(), goods.getImage2(),
                goods.getPrice(), goods.getIntro(), goods.getStock(), goods.getTypeid());
    }

    public void update(Goods goods) throws SQLException {
        QueryRunner r = new QueryRunner(JDBCUtils.getDataSource());
        String sql = "update goods set name=?,cover=?,image1=?,image2=?,price=?,intro=?,stock=?,type_id=? where id=?";
        r.update(sql, goods.getName(), goods.getCover(), goods.getImage1(), goods.getImage2(),
                goods.getPrice(), goods.getIntro(), goods.getStock(), goods.getTypeid(), goods.getId());
    }

    public void delete(int id) throws SQLException {
        QueryRunner r = new QueryRunner(JDBCUtils.getDataSource());
        String sql = "delete from goods where id=?";
        r.update(sql, id);
    }

    private int normalizeOffset(int pageNumber, int pageSize) {
        int safePageNumber = pageNumber < 1 ? 1 : pageNumber;
        int safePageSize = pageSize < 1 ? 8 : pageSize;
        return (safePageNumber - 1) * safePageSize;
    }
}
