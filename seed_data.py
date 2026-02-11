import csv
import logging
from datetime import datetime

from app import create_app, db
from app.models import Ingredients

# ロギング設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def seed_data():
    """CSVファイルからデータベースにデータを投入する。"""
    app = create_app()
    with app.app_context():
        # テーブル作成（念のため）
        db.create_all()

        csv_path = "resource/vegetable.csv"
        try:
            with open(csv_path, newline="", encoding="utf-8-sig") as csvfile:
                reader = csv.reader(csvfile)
                # ヘッダーがないため、そのまま読み込み開始（ID, Name, Date, Image, IsPresent）
                # もしヘッダーがある場合は next(reader) を実行するが、ファイル内容を見る限りヘッダーなし
                # しかし、docs/MySQL.md にはフィールド定義がある
                # ファイル内容: 1001,トマト,2023/11/4,tomato.png,1 -> ヘッダーなしと判断

                count = 0
                for row in reader:
                    if not row:
                        continue

                    try:
                        ingredient_id = int(row[0])
                        name = row[1]
                        expiration_date_str = row[2]
                        image_path = row[3]
                        is_present_val = row[4]

                        # NULL 文字列の処理
                        if expiration_date_str == "NULL":
                            expiration_date = None
                        else:
                            try:
                                expiration_date = datetime.strptime(
                                    expiration_date_str, "%Y/%m/%d"
                                ).date()
                            except ValueError:
                                logger.warning(
                                    f"Invalid date format: {expiration_date_str} for ID {ingredient_id}"
                                )
                                expiration_date = None

                        if is_present_val == "NULL":
                            is_present = 1  # Default
                        else:
                            try:
                                is_present = int(is_present_val)
                            except ValueError:
                                is_present = 1

                        # 既存データの確認（重複登録防止）
                        existing = Ingredients.query.get(ingredient_id)
                        if existing:
                            logger.info(
                                f"Updating existing ingredient: {name} (ID: {ingredient_id})"
                            )
                            existing.name = name
                            existing.expiration_date = expiration_date
                            existing.image_path = image_path
                            existing.is_present = is_present
                            existing.category = 1  # vegetable.csv contains vegetables
                        else:
                            ingredient = Ingredients(
                                IngredientID=ingredient_id,
                                name=name,
                                expiration_date=expiration_date,
                                image_path=image_path,
                                is_present=is_present,
                                category=1,  # vegetable.csv contains vegetables
                            )
                            db.session.add(ingredient)
                        count += 1

                    except (IndexError, ValueError) as e:
                        logger.error(f"Error processing row {row}: {e}")
                        continue

                db.session.commit()
                logger.info(f"Successfully added {count} ingredients.")

        except FileNotFoundError:
            logger.error(f"CSV file not found: {csv_path}")
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            db.session.rollback()


if __name__ == "__main__":
    seed_data()
