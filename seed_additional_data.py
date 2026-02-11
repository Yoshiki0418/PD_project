import csv
import logging

from app import create_app, db
from app.models import Ingredients

# ロギング設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def seed_additional_data():
    """追加の食材データCSVからデータベースにデータを投入する。"""
    app = create_app()
    with app.app_context():
        # テーブル作成（念のため）
        db.create_all()

        csv_path = "resource/additional_ingredients.csv"
        try:
            with open(csv_path, newline="", encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile)
                # ヘッダーなし: ID, Name, Date, Image, IsPresent, Category

                count = 0
                for row in reader:
                    if not row:
                        continue

                    try:
                        ingredient_id = int(row[0])
                        name = row[1]
                        # expiration_date_str = row[2] # NULL
                        image_path = row[3]
                        # is_present_val = row[4] # 1
                        category_val = int(row[5])

                        # expiration_date は NULL なので None
                        expiration_date = None
                        
                        # is_present は 0 に設定（在庫なし）
                        is_present = 0

                        # 既存データの確認（重複登録防止）
                        existing = Ingredients.query.get(ingredient_id)
                        if existing:
                            logger.info(
                                f"Updating existing ingredient: {name} (ID: {ingredient_id})"
                            )
                            existing.name = name
                            existing.image_path = image_path
                            existing.category = category_val
                            # is_present, expiration_date は既存のままにするか？
                            # 今回は新規追加が主目的なので、既存があれば更新するが、状態は保持したいかも
                            # しかし、Masterデータ更新と考えると上書きもあり。
                            # ここではカテゴリーと名前、画像を更新するにとどめる
                        else:
                            ingredient = Ingredients(
                                IngredientID=ingredient_id,
                                name=name,
                                expiration_date=expiration_date,
                                image_path=image_path,
                                is_present=is_present,
                                category=category_val,
                            )
                            db.session.add(ingredient)
                        count += 1

                    except (IndexError, ValueError) as e:
                        logger.error(f"Error processing row {row}: {e}")
                        continue

                db.session.commit()
                logger.info(f"Successfully processed {count} additional ingredients.")

        except FileNotFoundError:
            logger.error(f"CSV file not found: {csv_path}")
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            db.session.rollback()


if __name__ == "__main__":
    seed_additional_data()
